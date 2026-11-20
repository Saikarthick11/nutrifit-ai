export type Food = {name:string;quantity:number|null;unit:string|null};
export type NutrientKey = 'kcal'|'protein_g'|'carbs_g'|'fat_g';
export type Nutrients = Record<NutrientKey,number|null>;
export type Nutrition = {source?:'nutrition_label';fdc_id?:number;description:string;grams:number|null;portion_source:string;source_url?:string;nutrients:Nutrients};
export type Draft = {intent:string;date:string|null;end_date:string|null;foods:Food[];workouts:{name:string;duration_minutes:number|null}[]};
export type Entry = {id:string;date:string;extraction:Draft;nutrition:Record<string,Nutrition>};
export type History = {start:string;end:string;known_totals:Record<NutrientKey,number>;foods_missing_nutrients:Record<NutrientKey,number>;records:Entry[]};
export type Conversation = {label_review?:Record<string,unknown>;edit_source?:string;edit_source_version?:number;id:string;version:number;mode:'baseline'|'llm';status:string;reply:string;messages:{role:string;content:string}[];extraction:Draft|null;nutrition:Record<string,Nutrition>;history?:History};
export type Config = {llm_configured:boolean;usda_configured:boolean;llm_provider:string;llm_model:string;database:string;timezone:string};
export const nutrientKeys:NutrientKey[]=['kcal','protein_g','carbs_g','fat_g'];
export const nutrientLabels:Record<NutrientKey,string>={kcal:'Calories',protein_g:'Protein',carbs_g:'Carbs',fat_g:'Fat'};
export function dateInZone(timezone:string,now=new Date()):string {
 const parts=new Intl.DateTimeFormat('en-US',{timeZone:timezone,year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(now);
 const part=(name:string)=>parts.find(p=>p.type===name)!.value;
 return `${part('year')}-${part('month')}-${part('day')}`;
}
export function shiftDate(day:string,offset:number):string {
 const d=new Date(day+'T12:00:00Z');d.setUTCDate(d.getUTCDate()+offset);return d.toISOString().slice(0,10);
}
export function dateLabel(day:string,short=false):string {
 return new Intl.DateTimeFormat('en-US',{timeZone:'UTC',...(short?{weekday:'short'}:{weekday:'long',month:'short',day:'numeric'})}).format(new Date(day+'T12:00:00Z'));
}
export function summarize(entries:Entry[]) {
 const totals=Object.fromEntries(nutrientKeys.map(k=>[k,0])) as Record<NutrientKey,number>;
 const missing={...totals},known={...totals};
 let meals=0,workouts=0,minutes=0,foods=0;
 for(const entry of entries){
  if(entry.extraction.intent==='meal_log'){
   meals++;
   for(let i=0;i<entry.extraction.foods.length;i++){
    foods++;
    for(const k of nutrientKeys){const value=entry.nutrition[String(i)]?.nutrients[k];if(typeof value==='number'&&Number.isFinite(value)){totals[k]+=value;known[k]++;}else missing[k]++;}
   }
  }
  if(entry.extraction.intent==='workout_log'){
   workouts+=entry.extraction.workouts.length;
   minutes+=entry.extraction.workouts.reduce((sum,w)=>sum+(w.duration_minutes??0),0);
  }
 }
 return {totals,missing,known,meals,workouts,minutes,foods};
}
export function weekSeries(entries:Entry[],end:string){return Array.from({length:7},(_,i)=>{const day=shiftDate(end,i-6);return {day,...summarize(entries.filter(r=>r.date===day))};});}
export async function api<T>(path:string,body?:unknown):Promise<T>{
 let response:Response;
 try {response=await fetch('/api'+path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});}catch{throw new Error('Unable to connect. Please try again in a moment.');}
 let data:any;
 try{data=await response.json();}catch{throw new Error('The service is unavailable. Please try again in a moment.');}
 if(!response.ok)throw new Error(typeof data.detail==='string'?data.detail:'Please check the entered values.');
 return data as T;
}
