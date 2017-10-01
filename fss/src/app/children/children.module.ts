import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';
import { FormsModule } from '@angular/forms';

import { ChildrenPage } from './children-page.component';
import { ChildDetails } from './child-details.component';
import { ChildList } from './child-list.component';
import { ChildTabs } from './child-tabs.component';

import { FamilyTabComponent } from './tabs/family-info-tab.component';
import { FamilyListComponent } from './tabs/family-list.component';
import { MedicalTabComponent } from './tabs/medical-info-tab.component';
import { InteractionsTabComponent } from './tabs/interactions-tab.component';
import { InteractionsFormComponent } from './tabs/interactions-form.component';
import { ProjectedPathwayTabComponent } from './tabs/projected-pathway-tab.component';

@NgModule({
	declarations: [
		ChildrenPage,
		ChildList,
		ChildDetails,
		ChildTabs,
		FamilyTabComponent,
		FamilyListComponent,
		MedicalTabComponent,
		InteractionsTabComponent,
		InteractionsFormComponent,
		ProjectedPathwayTabComponent
	],
	imports: [
		BrowserModule,
		MaterialModule,
		FormsModule
	],
	providers: [],
	bootstrap: [ChildrenPage]
})
export class ChildrenModule { }
