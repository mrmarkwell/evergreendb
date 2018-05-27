import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { SettingsPage, PasswordChangeDialog } from './settings-page.component';
import { AdminPage, AddUserDialog } from './admin-settings-page.component';
import { LoginPage } from '../login/login-page.component';
import { RestService } from '../rest.service'
import { MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSlideToggleModule,
    MatDialogModule,
    MatListModule,
    MatTableModule,
    MatCheckboxModule} from '@angular/material';
import { FormsModule } from '@angular/forms';
@NgModule({
	declarations: [
        SettingsPage,
        LoginPage,
        PasswordChangeDialog,
        AdminPage,
        AddUserDialog
	],
	imports: [
        BrowserModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        FormsModule,
        MatSlideToggleModule,
        MatDialogModule,
        MatListModule,
        MatTableModule,
        MatCheckboxModule
	],
	providers: [
        RestService
    ],
    bootstrap: [SettingsPage],
    entryComponents: [PasswordChangeDialog, AddUserDialog]
})
export class SettingsModule {



}
