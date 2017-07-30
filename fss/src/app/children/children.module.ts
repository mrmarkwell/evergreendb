import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';

import { ChildrenTab } from './children-tab.component';
import { ChildDetails } from './child-details.component';
import { ChildList } from './child-list.component';
import { ChildTabs } from './child-tabs.component';

@NgModule({
	declarations: [
		ChildrenTab,
		ChildList,
		ChildDetails,
		ChildTabs
	],
	imports: [
		BrowserModule,
		MaterialModule
	],
	providers: [],
	bootstrap: [ChildrenTab]
})
export class ChildrenModule { }