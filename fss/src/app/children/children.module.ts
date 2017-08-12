import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';

import { ChildrenTab } from './children-tab.component';
import { ChildDetails } from './child-details.component';
import { ChildList } from './child-list.component';
import { ChildTabs } from './child-tabs.component';

import { FamilyTabComponent } from './tabs/family-info-tab.component';
import { MedicalTabComponent } from './tabs/medical-info-tab.component';
import { InteractionsTabComponent } from './tabs/interactions-tab.component';
import { ProjectedPathwayTabComponent } from './tabs/projected-pathway-tab.component';

@NgModule({
	declarations: [
		ChildrenTab,
		ChildList,
		ChildDetails,
		ChildTabs,
		FamilyTabComponent,
		MedicalTabComponent,
		InteractionsTabComponent,
		ProjectedPathwayTabComponent
	],
	imports: [
		BrowserModule,
		MaterialModule
	],
	providers: [],
	bootstrap: [ChildrenTab]
})
export class ChildrenModule { }
