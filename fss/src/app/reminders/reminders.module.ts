import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { RemindersTab } from './reminders-tab.component';
import { ReminderList } from './reminder-list.component';

import { MatListModule,
	MatExpansionModule } from '@angular/material';

@NgModule({
	declarations: [
		RemindersTab,
		ReminderList
	],
	imports: [
		BrowserModule,
		MatListModule,
		MatExpansionModule
	],
	providers: [],
	bootstrap: [ReminderList]
})
export class RemindersModule { }
