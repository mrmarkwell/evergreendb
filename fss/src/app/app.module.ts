import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';

import { ChildrenTab } from './children/children-tab.component';
import { RemindersTab } from './reminders/reminders-tab.component';
import { CalendarTab } from './calendar/calendar-tab.component';
import { SettingsTab } from './settings/settings-tab.component';

@NgModule({
	declarations: [
		AppComponent,
		ChildrenTab,
		RemindersTab,
		CalendarTab,
		SettingsTab
	],
	imports: [
		BrowserModule,
		AppRoutingModule,
		MaterialModule
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule { }
