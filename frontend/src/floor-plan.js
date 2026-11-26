import {el} from './dom.js';
import {request} from './api.js';

const ns = 'http://www.w3.org/2000/svg';

function mark(kind, attributes, label) {
  const object = document.createElementNS(ns,kind);
  for (const [key,value] of Object.entries(attributes)) object.setAttribute(key,value);
  if (label) object.textContent = label;
  return object;
}

function drawing(panels, points, restricted, shift) {
  const width = Math.max(600,...panels.map((panel)=>panel.x2));
  const height = Math.max(600,...panels.map((panel)=>panel.y2));
  const canvas = mark('svg',{viewBox:'-9 -9 '+(width+18)+' '+(height+18),role:'img',
    'aria-label':'舞室胶带分区及 '+shift+' 停练与量测点'});
  for (const panel of panels) {
    const shut = restricted.some((hold)=>hold.shift===shift&&hold.panel===panel.code&&hold.status==='停练');
    canvas.append(mark('rect',{x:panel.x1,y:panel.y1,width:panel.x2-panel.x1,height:panel.y2-panel.y1,
      class:shut?'closed-zone':'zone'}));
    canvas.append(mark('text',{x:panel.x1+15,y:panel.y1+26},panel.code+(shut?' 停练':'')));
  }
  for (const point of points) {
    const panel=panels.find((panel)=>panel.code===point.panel);
    if (!point.checked||!panel) continue;
    const tag=mark('circle',{cx:point.x_cm,cy:point.y_cm,r:8,class:point.slide<panel.control_band?'low':'ordinary'});
    tag.append(mark('title',{},point.code+' · '+point.survey+' · '+point.slide));
    canvas.append(tag);
  }
  return canvas;
}

export async function floorPlan(root) {
  const [panels,points,holds,classes]=await Promise.all([request('/studio_panels'),
    request('/floor_readings'),request('/practice_holds'),request('/dance_blocks')]);
  const shifts=[...new Set([...holds,...classes].map((item)=>item.shift))].sort();
  const selector=el('select',{'aria-label':'地图课程时段'},
    shifts.map((shift)=>el('option',{value:shift},shift)));
  if(shifts.includes('EV-02')) selector.value='EV-02';
  const chart=el('div',{});
  const figure=el('figure',{class:'floor-plan'},el('figcaption',{},'胶带边界与踏点平面'),selector,chart,
    el('small',{},'粉色圆点为单列读数，蓝点为常规读数。深粉区域为该班次围挡。'));
  function render() { chart.replaceChildren(drawing(panels,points,holds,selector.value)); }
  selector.addEventListener('change',render);
  root.querySelector('.ledger')?.before(figure);
  render();
}
