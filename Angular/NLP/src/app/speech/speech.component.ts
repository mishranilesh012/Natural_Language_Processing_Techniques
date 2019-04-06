import { Component, OnInit } from '@angular/core';
import {AuthService} from '../auth.service';
import { Http } from '@angular/http';

@Component({
  selector: 'app-speech',
  templateUrl: './speech.component.html',
  styleUrls: ['./speech.component.css']
})
export class SpeechComponent implements OnInit {

  base64textString:any;
  imageData:any;
  ocr:any;
  val:any;
  arg:any;
  arr:any[];
  str: string;
  constructor(http: Http,  private authService: AuthService) { }

  ngOnInit() {
  }

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
    imageData:this.ocr,
    text:this.str
  }

  console.log(ocrString);
  this.authService.sendOcrDetails(ocrString).subscribe(data => {
    this.arr = data;
    this.arr = Array.of(this.arr);
     console.log(this.arr[0]);

  });
 }

}
