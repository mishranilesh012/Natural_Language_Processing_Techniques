import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import {AuthService} from './auth.service';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { OcrComponent } from './ocr/ocr.component';
import { SpeechComponent } from './speech/speech.component';

const appRoutes: Routes = [
  {
    path: '',
    component: OcrComponent
  },
  {
    path: 'ocr',
    component: OcrComponent
  },
  {
    path: 'speech',
    component: SpeechComponent
  }
]

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    OcrComponent,
    SpeechComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    RouterModule.forRoot(appRoutes),
    FormsModule,
    NgbModule
  ],
  providers: [AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
