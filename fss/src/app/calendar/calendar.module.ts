import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';

import { CalendarTab } from './calendar-tab.component';

@NgModule({
	declarations: [
		CalendarTab
	],
	imports: [
		BrowserModule,
		MaterialModule
	],
	providers: [],
	bootstrap: [CalendarTab]
})
export class CalendarModule { }
