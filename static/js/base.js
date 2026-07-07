"use strict";

const storage={get(key){try{return window.localStorage.getItem(key)}catch(_){return null}},set(key,value){try{window.localStorage.setItem(key,value)}catch(_){}}};
const themes={forest:{name:"Forest",mode:"Dark",description:"Deep botanical green and gold.",side:"#061f19",main:"#081a17",accent:"#a9c979"},moonlit:{name:"Moonlit",mode:"Dark",description:"Celestial navy, periwinkle and gold.",side:"#0a0f20",main:"#0c1123",accent:"#9fb5ff"},clay:{name:"Clay",mode:"Dark",description:"Charcoal, terracotta and warm gold.",side:"#211512",main:"#211513",accent:"#e39a72"},daybreak:{name:"Daybreak",mode:"Light",description:"Mist blue, periwinkle and gold.",side:"#dfe4f0",main:"#eef1f8",accent:"#6078bb"},linen:{name:"Linen",mode:"Light",description:"Paper neutrals, sage and warm gold.",side:"#e5dfd3",main:"#efebe2",accent:"#56745e"},harvest:{name:"Harvest",mode:"Light",description:"Warm cream, terracotta and gold.",side:"#e3d2c4",main:"#f2e8de",accent:"#a45e43"}};

const sidebar=document.querySelector("#sidebar");
const menuButton=document.querySelector("#menu-button");
const scrim=document.querySelector("#sidebar-scrim");
const themePanel=document.querySelector("#theme-panel");
const themeButton=document.querySelector("#theme-button");
const themeClose=document.querySelector("#theme-close");
const toastRegion=document.querySelector("#toast-region");
const mobileNavigation=window.matchMedia("(max-width: 900px)");

function buildThemePanel(){
  ["dark","light"].forEach(mode=>{
    const root=document.querySelector(`[data-theme-group="${mode}"]`);
    if(!root)return;
    root.innerHTML=Object.entries(themes)
      .filter(([,theme])=>theme.mode.toLowerCase()===mode)
      .map(([key,theme])=>`<button class="theme-choice" type="button" data-set-theme="${key}" style="--p-side:${theme.side};--p-main:${theme.main};--p-accent:${theme.accent}"><span class="theme-choice-preview"><aside></aside><main><i></i><i></i></main></span><b>${theme.name}</b><small>${theme.description}</small></button>`)
      .join("");
  });
}

function syncThemeUI(){
  const current=document.documentElement.dataset.theme||"moonlit";
  document.querySelectorAll("[data-set-theme]").forEach(button=>button.classList.toggle("active",button.dataset.setTheme===current));
}

function toast(title,message){
  if(!toastRegion)return;
  const element=document.createElement("div");
  element.className="toast";
  element.innerHTML=`<b>${title}</b><span>${message}</span>`;
  toastRegion.appendChild(element);
  window.setTimeout(()=>element.remove(),3200);
}

function setTheme(name,notify=true){
  if(!themes[name])return;
  document.documentElement.dataset.theme=name;
  storage.set("ceres-theme",name);
  syncThemeUI();
  if(notify)toast("Theme changed",`${themes[name].name} is now active across Ceres.`);
}

function openThemes(){
  if(!themePanel||!themeButton)return;
  themePanel.hidden=false;
  themeButton.setAttribute("aria-expanded","true");
  syncThemeUI();
}

function closeThemes(){
  if(!themePanel||!themeButton)return;
  themePanel.hidden=true;
  themeButton.setAttribute("aria-expanded","false");
}

function setSidebarOpen(isOpen,restoreFocus=false){
  if(!sidebar||!menuButton||!scrim)return;
  const shouldOpen=mobileNavigation.matches&&isOpen;
  sidebar.classList.toggle("open",shouldOpen);
  scrim.classList.toggle("visible",shouldOpen);
  scrim.setAttribute("aria-hidden",String(!shouldOpen));
  menuButton.setAttribute("aria-expanded",String(shouldOpen));
  document.body.classList.toggle("navigation-open",shouldOpen);
  if(mobileNavigation.matches){
    sidebar.toggleAttribute("inert",!shouldOpen);
    sidebar.setAttribute("aria-hidden",String(!shouldOpen));
  }else{
    sidebar.removeAttribute("inert");
    sidebar.removeAttribute("aria-hidden");
  }
  if(!shouldOpen&&restoreFocus)menuButton.focus();
}

menuButton?.addEventListener("click",()=>setSidebarOpen(true));
scrim?.addEventListener("click",()=>setSidebarOpen(false,true));
sidebar?.querySelectorAll("a").forEach(link=>link.addEventListener("click",()=>setSidebarOpen(false)));
themeButton?.addEventListener("click",()=>themePanel?.hidden?openThemes():closeThemes());
themeClose?.addEventListener("click",closeThemes);

document.addEventListener("click",event=>{
  const themeTarget=event.target.closest("[data-set-theme]");
  if(themeTarget)setTheme(themeTarget.dataset.setTheme);
});

document.addEventListener("keydown",event=>{
  if(event.key==="Escape"){
    closeThemes();
    setSidebarOpen(false,true);
  }
  if(event.key==="/"&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName)){
    event.preventDefault();
    const searchUrl=document.body.dataset.searchUrl;
    if(searchUrl)window.location.assign(searchUrl);
  }
});

mobileNavigation.addEventListener("change",()=>setSidebarOpen(false));
buildThemePanel();
setTheme(storage.get("ceres-theme")||"moonlit",false);
setSidebarOpen(false);
