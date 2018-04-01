import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { SettingsPage, PasswordChangeDialog } from './settings-page.component';
import { LoginPage } from '../login/login-page.component';
import { RestService } from '../rest.service'
import { MatFormFieldModule, MatInputModule, MatButtonModule, MatSlideToggleModule, MatDialogModule } from '@angular/material';
import { FormsModule } from '@angular/forms';
@NgModule({
	declarations: [
        SettingsPage,
        LoginPage,
        PasswordChangeDialog
	],
	imports: [
        BrowserModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        FormsModule,
        MatSlideToggleModule,
        MatDialogModule
	],
	providers: [
        RestService
    ],
    bootstrap: [SettingsPage],
    entryComponents: [PasswordChangeDialog]
})
export class SettingsModule { 



}
