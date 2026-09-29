// Three.js interactive 3D particle field
const wrap=document.getElementById("canvas-wrap");
if(window.THREE && wrap){
 const scene=new THREE.Scene();
 const camera=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,100);
 camera.position.z=7;
 const renderer=new THREE.WebGLRenderer({alpha:true,antialias:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.setSize(innerWidth,innerHeight); wrap.appendChild(renderer.domElement);
 const geo=new THREE.BufferGeometry(), count=900, pos=new Float32Array(count*3);
 for(let i=0;i<count;i++){const r=7*Math.pow(Math.random(),.55),a=Math.random()*Math.PI*2,b=(Math.random()-.5)*2;pos[i*3]=Math.cos(a)*r;pos[i*3+1]=b*r*.55;pos[i*3+2]=Math.sin(a)*r;}
 geo.setAttribute("position",new THREE.BufferAttribute(pos,3));
 const mat=new THREE.PointsMaterial({color:0x5da7ff,size:.018,transparent:true,opacity:.55});
 const stars=new THREE.Points(geo,mat);scene.add(stars);
 const torus=new THREE.Mesh(new THREE.TorusGeometry(2.8,.006,12,180),new THREE.MeshBasicMaterial({color:0x3e8cff,transparent:true,opacity:.28}));
 torus.rotation.x=Math.PI/2.4;scene.add(torus);
 let mx=0,my=0; addEventListener("mousemove",e=>{mx=(e.clientX/innerWidth-.5)*.5;my=(e.clientY/innerHeight-.5)*.3});
 function animate(){requestAnimationFrame(animate);stars.rotation.y+=.0005;stars.rotation.x+=.00015;torus.rotation.z+=.001;camera.position.x+=(mx-camera.position.x)*.03;camera.position.y+=(-my-camera.position.y)*.03;camera.lookAt(0,0,0);renderer.render(scene,camera)}
 animate();addEventListener("resize",()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});
}
const menu=document.querySelector(".menu"),nav=document.querySelector("nav");menu?.addEventListener("click",()=>{nav.style.display=nav.style.display==="flex"?"none":"flex";nav.style.position="absolute";nav.style.top="76px";nav.style.left="0";nav.style.right="0";nav.style.padding="20px";nav.style.background="#06090fcc";nav.style.flexDirection="column"});
document.getElementById("form")?.addEventListener("submit",e=>{e.preventDefault();alert("Demo registration submitted. Connect a backend/database to store real registrations.");});
