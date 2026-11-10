let generator=null,TextStreamer=null,loading=false;
const post=(type,extra={})=>self.postMessage({type,...extra});
self.onmessage=async({data})=>{try{
 if(data.type==='load'){
  if(loading||generator)return;loading=true;
  const lib=await import('https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1/dist/transformers.min.js');
  TextStreamer=lib.TextStreamer;lib.env.allowLocalModels=false;lib.env.backends.onnx.wasm.numThreads=1;
  let device='wasm';
  if(data.device==='auto'&&self.navigator.gpu){try{if(await self.navigator.gpu.requestAdapter())device='webgpu';}catch{}}
  const options={dtype:'q4',device,progress_callback:p=>{if(p.status==='progress')post('progress',{file:p.file,progress:p.progress});}};
  post('status',{text:'모델 파일을 확인하고 있습니다. 첫 실행에는 시간이 걸립니다.'});
  try{generator=await lib.pipeline('text-generation','onnx-community/Qwen2.5-0.5B-Instruct',options);}
  catch(error){if(device!=='webgpu')throw error;post('status',{text:'GPU 실행이 어려워 호환 모드로 전환합니다.'});device='wasm';generator=await lib.pipeline('text-generation','onnx-community/Qwen2.5-0.5B-Instruct',{...options,device});}
  loading=false;post('ready',{device});
 }
 if(data.type==='generate'){
  if(!generator)throw Error('모델이 준비되지 않았습니다.');
  const start=performance.now();
  const streamer=new TextStreamer(generator.tokenizer,{skip_prompt:true,skip_special_tokens:true,callback_function:text=>post('token',{text})});
  const output=await generator(data.messages,{max_new_tokens:160,do_sample:false,repetition_penalty:1.1,streamer});
  const generated=output[0].generated_text;
  const text=Array.isArray(generated)?generated[generated.length-1].content:generated;
  post('done',{text,seconds:(performance.now()-start)/1000});
 }
}catch(error){loading=false;post('error',{message:error.message||String(error)});}};
