import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { RemindersTab } from './reminders-tab.component';

@NgModule({
	declarations: [
		RemindersTab
	],
	imports: [
		BrowserModule,
	],
	providers: [],
	bootstrap: [RemindersTab]
})
export class RemindersModule { }
