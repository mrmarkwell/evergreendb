import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { SettingsPage } from './settings-page.component';
import { LoginPage } from '../login/login-page.component';
import { RestService } from '../rest.service'
import { MatFormFieldModule, MatInputModule, MatButtonModule, MatSlideToggleModule} from '@angular/material';
import { FormsModule } from '@angular/forms';
@NgModule({
	declarations: [
        SettingsPage,
        LoginPage,
	],
	imports: [
        BrowserModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        FormsModule,
        MatSlideToggleModule
	],
	providers: [
        RestService
    ],
	bootstrap: [SettingsPage]
})
export class SettingsModule { 



}
