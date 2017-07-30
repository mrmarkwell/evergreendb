import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';

import { RemindersTab } from './reminders-tab.component';

@NgModule({
	declarations: [
		RemindersTab
	],
	imports: [
		BrowserModule,
		MaterialModule
	],
	providers: [],
	bootstrap: [RemindersTab]
})
export class RemindersModule { }
