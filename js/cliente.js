//DADOS
const http = new XMLHttpRequest();
const url='http://192.168.1.3:5001/';

function setRequest(){
  http.setRequestHeader('Access-Control-Allow-Origin', '*');
  http.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, LIST, OPTIONS, PUT, PATCH, DELETE');
  http.setRequestHeader('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers');
}

var listaMusicas = null //variável contém nomes das músicas no diretório do servidor


//lista todas as músicas contidas no servidor
function listarMusicas(){
  //FILTRAR SÓ PRA TER ARQUIVOS MP3 - FAZER ISSO NO SERVER
  http.open("LIST", url)
  //setRequest();
  http.send("");
  http.onreadystatechange = (e) => {
      listaMusicas = http.responseText.split(",")
      console.log(listaMusicas.length) 
      var lista = document.getElementById("lista")
      if (lista!=null){
        lista.innerHTML = "" //garante que lista não será duplicada no html ao ser atualizada
        for (var i=0; i<listaMusicas.length; i++){
          document.getElementById("lista").innerHTML +=
          '<div class="player2 row text-primary">' + '<div class="col-sm-1">' + 
          '<img src="images/icons/music.png" width="30" height="30" alt="iconemusica"> </div>' + 
          `<div class="col-sm-8"onclick="selecionarMusica(${listaMusicas[i]})">${listaMusicas[i].toUpperCase().replace(".MP3","").substring(1, listaMusicas[i].length-1)}</div>` +
          `<div class="col-sm-1"> <a href="Musicas/${listaMusicas[i].substring(1, listaMusicas[i].length-1)}" download>Baixar música</a> </div> </div>`
          console.log(listaMusicas[i].substring(1, listaMusicas[i].length-1))
        }
      }
  }
}

function selecionarMusica(nomeMusica){
  console.log(nomeMusica)
  document.getElementById("musicao").innerHTML ='<audio id="audio" controls>' +
  `<source src="Musicas/${nomeMusica}" type="audio/mpeg"></source>'</audio>`
}


//Método que conecta-se com servidor e envia música
function uploadMusica(){
  var status = false;
  for(var i=0; i<20; i++){
    if(!status){
      var diretorio = document.getElementById("dirArquivo")
      if(diretorio.files.length!=0){

        var porcentagem = 0
          var file = diretorio.files[0]//recebo objeto do tipo file
          var formData = new FormData();
    
          formData.append(file.name, file)
          http.open("POST", url +file.name)
          http.setRequestHeader('Content-type', "application/x-www-form-urlencoded; charset=UTF-8");
    
          //para fazer o progress bar no html
          http.upload.addEventListener("progress", function (event) {
    
            if (event.lengthComputable) {
              porcentagem = event.loaded / event.total * 100; //faz 
              document.getElementById("lista").innerHTML = '<div class="progress">' +
                `<div class="progress-bar progress-bar-striped" role="progressbar" style="width: ${porcentagem}%"` + 
                'aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div> </div>'
            }
        });
        http.send(formData)
        status=true;
      } else{
        alert("Você precisa selecionar um arquivo para enviar!")
      }
    }
  }
  //recebe arquivo selecionado - nesse caso só há 1
}




//BOTÕES DO TOPO


//Página para envio de música
function enviarMusica(){
  document.getElementById("main").innerHTML ='<div class="my-12"></div>' +'<h2 class="display-4 text-primary my-5">Enviar música</h2>' +
  '<h3 class="display-6 text-light">Selecione o diretório para upload da música. O arquivo deve estar no formato .MP3</h3>' +
  `<input id="dirArquivo" class="my-5" type='file' accept='audio/mp3' id='file-input' />`+ `<button id="enviar" onclick="uploadMusica()" type="button" class="btn btn-primary my-5">Enviar música</button>`
  + '<div id="lista"></div>'
  
}

function sobre(){
  document.getElementById("main").innerHTML ='<h2 class="display-4 text-primary my-12">Sobre</h2>' +
  '<h3 class="display-6 text-light">Alfred Music, é uma aplicação desenvolvida pelos alunos da disciplina de RDC 1.</h3>' +
  '<div class="player2 row text-primary">MATHEUS PHELIPE ALVES PINTO</div>' +
  '<div class="player2 row text-primary">MURILO CAMPANHOL STODOLNI</div>' +
  '<div class="player2 row text-primary">NILTON VIEIRA DA SILVA</div>' +
  '<div class="player2 row text-primary">RICHARD JEREMIAS MARTINS ROCHA</div>' +
  `<h3 class="display-6 text-primary">Quantidade de músicas disponíveis: ${listaMusicas.length}</h3>`
}
//exibe lista com todas as músicas
function todasMusicas(){
  document.getElementById("main").innerHTML = '<h2 class="display-4 text-primary">Todas as músicas</h2>' + `<div id="lista" class="text-dark"></div>`
  listarMusicas()
}


/*function uploadMusica(){
  
  //recebe arquivo selecionado - nesse caso só há 1
  var diretorio = document.getElementById("dirArquivo")
  document.getElementById("lista").innerHTML = '<div class="player2 row text-primary">' + 'Seu arquivo está sendo enviado</div>'
  if(diretorio.files.length!=0){
    var file = diretorio.files[0]//recebo objeto do tipo file
      var formData = new FormData();
      formData.append(file.name, file)
      http.open("POST", file.name)
      setRequest()
      http.setRequestHeader('Content-type','application/json; charset=utf-8');
      //Http.setRequestHeader('Content-type', 'multipart/form-data');
      http.send(formData)
  }else{
    alert("Você precisa selecionar um arquivo para enviar!")
  }
}*/