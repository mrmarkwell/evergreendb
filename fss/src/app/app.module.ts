import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MatNativeDateModule,
    MatIconModule,
    MatSidenavModule } from '@angular/material';
import { HttpClientModule } from '@angular/common/http'

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
//import { HttpModule } from '@angular/http';
import { DatePipe } from '@angular/common';

import { RestService } from './rest.service';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { CalendarModule } from './calendar/calendar.module';
import { ChildrenModule } from './children/children.module';
import { RemindersModule } from './reminders/reminders.module';
import { SettingsModule } from './settings/settings.module';

@NgModule({
	declarations: [
		AppComponent
	],
	imports: [
		BrowserModule,
		AppRoutingModule,
		//HttpModule,
        HttpClientModule,
		MatNativeDateModule,
        MatIconModule,
        MatSidenavModule,
		BrowserAnimationsModule,
		CalendarModule,
		ChildrenModule,
		RemindersModule,
		SettingsModule,
	],
	providers: [
		RestService,
		DatePipe,
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
