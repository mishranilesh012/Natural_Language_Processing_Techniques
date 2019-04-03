import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'NLP';
  base64textString:any;
  imageData:any;
  ocr:any;
  val:any;
  arg:any;


  selectFile(event){
    var files = event.target.files;
    var file = files[0];

  if (files && file) {
      var reader = new FileReader();

      reader.onload =this.handleFile.bind(this);

      reader.readAsBinaryString(file);
  }
}

handleFile(event) {
  var binaryString = event.target.result;
         this.base64textString= btoa(binaryString);
         //console.log(btoa(binaryString));
         this.imageData = btoa(binaryString);

 }
 sendString(){
  this.ocr = this.imageData;

  const ocrString = {
    imageData:this.ocr
  }

  console.log(ocrString);
 }



}
