import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { SettingsTab } from './settings-tab.component';
import { LoginPage } from '../login/login-page.component';
import { RestService } from '../rest.service'
import { MatFormFieldModule, MatInputModule, MatButtonModule } from '@angular/material';
import { FormsModule } from '@angular/forms';
@NgModule({
	declarations: [
        SettingsTab,
        LoginPage,
	],
	imports: [
        BrowserModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        FormsModule
	],
	providers: [
        RestService
    ],
	bootstrap: [SettingsTab]
})
export class SettingsModule { }
