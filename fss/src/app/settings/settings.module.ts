import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { SettingsTab } from './settings-tab.component';

@NgModule({
	declarations: [
		SettingsTab
	],
	imports: [
		BrowserModule,
	],
	providers: [],
	bootstrap: [SettingsTab]
})
export class SettingsModule { }
