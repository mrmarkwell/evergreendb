import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';

import { ChildrenTab } from './children/children-tab.component';
import { RemindersTab } from './reminders/reminders-tab.component';

@NgModule({
	declarations: [
		AppComponent,
		ChildrenTab,
		RemindersTab
	],
	imports: [
		BrowserModule,
		AppRoutingModule
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule { }
