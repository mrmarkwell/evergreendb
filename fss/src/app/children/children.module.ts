import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';

import { ChildrenTab } from './children-tab.component';

@NgModule({
	declarations: [
		ChildrenTab
	],
	imports: [
		BrowserModule,
		MaterialModule
	],
	providers: [],
	bootstrap: [ChildrenTab]
})
export class ChildrenModule { }
