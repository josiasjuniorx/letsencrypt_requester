function toggleVisible(id){
  var estado = document.getElementById(id).style.display;
  if (estado == '' || estado == 'none') {
    document.getElementById(id).style.display = 'flex';
  }
  else {
    document.getElementById(id).style.display = 'none';
  }
}

function copyContent(id) {
  var conteudo = document.getElementById(id).innerHTML;
  var copySpace = document.createElement("textarea");
  document.body.appendChild(copySpace);
  copySpace.setAttribute("id", "copySpace");
  document.getElementById("copySpace").value=conteudo;
  copySpace.select();
  document.execCommand("copy");
  document.body.removeChild(copySpace);
}
