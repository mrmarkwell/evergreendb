import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';

import { SettingsTab } from './settings-tab.component';

@NgModule({
	declarations: [
		SettingsTab
	],
	imports: [
		BrowserModule,
		MaterialModule
	],
	providers: [],
	bootstrap: [SettingsTab]
})
export class SettingsModule { }
