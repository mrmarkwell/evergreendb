import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { CalendarTab } from './calendar-tab.component';

@NgModule({
	declarations: [
		CalendarTab
	],
	imports: [
		BrowserModule,
	],
	providers: [],
	bootstrap: [CalendarTab]
})
export class CalendarModule { }
