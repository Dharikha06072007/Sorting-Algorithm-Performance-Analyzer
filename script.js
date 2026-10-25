const $ = (id) => document.getElementById(id);
const names = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"];
let latestResults = [];
let originalInput = [];

$("count").addEventListener("input", () => $("countValue").textContent = $("count").value);
$("randomBtn").addEventListener("click", () => {
  const n = Number($("count").value);
  const values = Array.from({length:n}, () => Math.floor(Math.random() * 999) + 1);
  $("numbers").value = values.join(", ");
  $("message").textContent = `${n} random values generated.`;
  $("message").style.color = "#16835d";
});
$("clearBtn").addEventListener("click", () => {
  $("numbers").value = "";
  $("message").textContent = "";
  $("resultsSection").classList.add("hidden");
  latestResults = [];
});
$("fileInput").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  try {
    const content = await file.text();
    const values = content.match(/[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?/g);
    if (!values || !values.length) throw new Error("No numeric values found in this file.");
    $("numbers").value = values.join(", ");
    $("message").textContent = `Loaded ${values.length} numeric values from ${file.name}.`;
    $("message").style.color = "#16835d";
  } catch (err) {
    $("message").textContent = err.message || "Could not read this file.";
    $("message").style.color = "#bd3b4a";
  }
});
$("runBtn").addEventListener("click", runAnalysis);
$("algorithmSelect").addEventListener("change", showSortedOutput);
$("downloadBtn").addEventListener("click", downloadCSV);
window.addEventListener("resize", () => { if (latestResults.length) drawChart(latestResults); });

function parseNumbers() {
  const raw = $("numbers").value.trim();
  if (!raw) throw new Error("Enter some numbers or generate a random dataset first.");
  const tokens = raw.split(/[\s,;]+/).filter(Boolean);
  const values = tokens.map(Number);
  if (values.some(v => !Number.isFinite(v))) throw new Error("Please enter only valid numeric values, separated by commas or spaces.");
  if (values.length > 5000) throw new Error("Please use 5,000 values or fewer for this browser demo.");
  return values;
}
function runAnalysis() {
  $("message").style.color = "#bd3b4a";
  try {
    originalInput = parseNumbers();
    const expected = [...originalInput].sort((a,b) => a-b);
    latestResults = [
      measure("Bubble Sort", bubbleSort),
      measure("Selection Sort", selectionSort),
      measure("Insertion Sort", insertionSort),
      measure("Merge Sort", mergeSort),
      measure("Quick Sort", quickSort)
    ].map(r => ({...r, correct: r.output.length === expected.length && r.output.every((v,i) => Object.is(v, expected[i]))}));
    $("message").textContent = "";
    $("resultsSection").classList.remove("hidden");
    $("datasetSize").textContent = originalInput.length.toLocaleString();
    $("datasetInfo").textContent = `${originalInput.length.toLocaleString()} values · identical input for every algorithm`;
    $("fastest").textContent = latestResults.reduce((a,b) => a.ms < b.ms ? a : b).name;
    $("resultsBody").innerHTML = latestResults.map(r => `<tr><td class="algo-name">${r.name}</td><td>${formatTime(r.ms)}</td><td>${r.comparisons.toLocaleString()}</td><td>${r.moves.toLocaleString()}</td><td class="${r.correct ? "correct" : ""}">${r.correct ? "✓ Yes" : "✕ No"}</td></tr>`).join("");
    drawChart(latestResults);
    showSortedOutput();
    $("resultsSection").scrollIntoView({behavior:"smooth", block:"start"});
  } catch (err) {
    $("message").textContent = err.message;
  }
}
function measure(name, fn) {
  const input = [...originalInput];
  const stats = {comparisons:0, moves:0};
  const start = performance.now();
  const output = fn(input, stats);
  const ms = performance.now() - start;
  return {name, ms, comparisons:stats.comparisons, moves:stats.moves, output};
}
function bubbleSort(a,s){for(let i=0;i<a.length-1;i++){let changed=false;for(let j=0;j<a.length-i-1;j++){s.comparisons++;if(a[j]>a[j+1]){[a[j],a[j+1]]=[a[j+1],a[j]];s.moves++;changed=true;}}if(!changed)break;}return a;}
function selectionSort(a,s){for(let i=0;i<a.length-1;i++){let min=i;for(let j=i+1;j<a.length;j++){s.comparisons++;if(a[j]<a[min])min=j;}if(min!==i){[a[i],a[min]]=[a[min],a[i]];s.moves++;}}return a;}
function insertionSort(a,s){for(let i=1;i<a.length;i++){let key=a[i],j=i-1;while(j>=0){s.comparisons++;if(a[j]>key){a[j+1]=a[j];s.moves++;j--;}else break;}a[j+1]=key;}return a;}
function mergeSort(a,s){if(a.length<=1)return a;const mid=Math.floor(a.length/2),left=mergeSort(a.slice(0,mid),s),right=mergeSort(a.slice(mid),s);let i=0,j=0,out=[];while(i<left.length&&j<right.length){s.comparisons++;if(left[i]<=right[j])out.push(left[i++]);else out.push(right[j++]);s.moves++;}while(i<left.length){out.push(left[i++]);s.moves++;}while(j<right.length){out.push(right[j++]);s.moves++;}return out;}
function quickSort(a,s){function sort(lo,hi){if(lo>=hi)return;const pivot=a[Math.floor((lo+hi)/2)];let i=lo,j=hi;while(i<=j){while(i<=hi){s.comparisons++;if(a[i]<pivot)i++;else break;}while(j>=lo){s.comparisons++;if(a[j]>pivot)j--;else break;}if(i<=j){if(i!==j){[a[i],a[j]]=[a[j],a[i]];s.moves++;}i++;j--;}}if(lo<j)sort(lo,j);if(i<hi)sort(i,hi);}sort(0,a.length-1);return a;}
function formatTime(ms){return ms < 1 ? ms.toFixed(4) : ms.toFixed(3);}
function showSortedOutput(){const r=latestResults.find(x=>x.name===$("algorithmSelect").value);if(!r)return;$("sortedOutput").textContent=r.output.length>400?`${r.output.slice(0,400).join(", ")} …\n\nShowing first 400 of ${r.output.length} sorted values.`:r.output.join(", ");$("outputStatus").textContent=r.correct?"✓ Sorted correctly":"✕ Check failed";}
function drawChart(results){
 const canvas=$("chart"),rect=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1;
 canvas.width=Math.max(280,rect.width)*dpr;canvas.height=245*dpr;
 const ctx=canvas.getContext("2d");ctx.scale(dpr,dpr);
 const w=canvas.width/dpr,h=canvas.height/dpr;ctx.clearRect(0,0,w,h);
 const left=94,right=14,top=18,bottom=18,plotW=w-left-right,rowH=(h-top-bottom)/results.length;
 const max=Math.max(...results.map(r=>r.ms),0.001);
 results.forEach((r,i)=>{const y=top+i*rowH;ctx.fillStyle="#53617d";ctx.font="11px DM Sans, Arial";ctx.textAlign="right";ctx.textBaseline="middle";ctx.fillText(r.name.replace(" Sort",""),left-10,y+rowH/2);
  ctx.fillStyle="#eef1fa";ctx.beginPath();ctx.roundRect(left,y+rowH*.24,plotW,rowH*.52,5);ctx.fill();
  const barW=Math.max(3,plotW*r.ms/max);const grad=ctx.createLinearGradient(left,0,left+barW,0);grad.addColorStop(0,"#4968e8");grad.addColorStop(1,"#8862e8");ctx.fillStyle=grad;ctx.beginPath();ctx.roundRect(left,y+rowH*.24,barW,rowH*.52,5);ctx.fill();
  ctx.fillStyle="#293754";ctx.font="10px DM Sans, Arial";ctx.textAlign="left";const label=formatTime(r.ms)+" ms";ctx.fillText(label,Math.min(left+barW+6,w-48),y+rowH/2);
 });
}
function downloadCSV(){
 if(!latestResults.length)return;
 const rows=[["Algorithm","Execution Time (ms)","Comparisons","Swaps / shifts","Correct"],...latestResults.map(r=>[r.name,r.ms.toFixed(6),r.comparisons,r.moves,r.correct?"Yes":"No"])];
 const csv=rows.map(row=>row.map(v=>`"${String(v).replace(/"/g,'""')}"`).join(",")).join("\r\n");
 const blob=new Blob([csv],{type:"text/csv;charset=utf-8;"}),url=URL.createObjectURL(blob),a=document.createElement("a");
 a.href=url;a.download="sorting_performance_results.csv";document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);
}
