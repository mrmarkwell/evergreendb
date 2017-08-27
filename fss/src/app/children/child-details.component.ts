import { Component, OnInit, OnChanges, Input } from '@angular/core';
import { ParamMap } from '@angular/router';
import { DatePipe } from '@angular/common';

import { Child } from '../child';
import { RestService } from '../rest.service';

@Component({
	selector: 'child-details',
	templateUrl: "./child-details.component.html",
	styleUrls: ["./child-details.component.css"]
})
export class ChildDetails implements OnInit, OnChanges {
	constructor(
		private restService: RestService,
		private datePipe: DatePipe
	) {}
	ngOnInit(): void {
		this.restService.getEnum("fss_medical_condition").then(conditions => this.medical_conditions = conditions);
	}
	ngOnChanges(): void {
		console.log(this.child_id);
		this.restService.getChild(this.child_id).then(child => {this.child = child; this.age = child.getAge()});
	}
	saveChild(): void {
		this.restService.updateChild(this.child);
	}
	deleteChild(): void {
		if (confirm("Are you sure you want to delete this child and all associated data?")) {
			this.restService.deleteChild(this.child.id);
			//TODO: Delete associated family members, pathways, and interactions
			this.restService.getFamilyMembers(this.child.id).then(fam_mems => {
				for (let member of fam_mems) {
					this.restService.deleteFamilyMember(member.id);
				}
			});
			this.restService.getInteractions(this.child.id).then(interactions => {
				for (let interaction of interactions) {
					this.restService.deleteFamilyMember(interaction.id);
				}
			});
			this.restService.getProjectedPathway(this.child.id).then(pathways => {
				for (let pathway of pathways) {
					this.restService.deleteFamilyMember(pathway.id);
				}
			});
			this.child = null;
		}
	}

	setDoB(date): void {
		console.log(date);
		this.child.birth_date = this.datePipe.transform(date, 'yyyy-MM-dd');
		console.log(this.child.birth_date);
		this.age = this.child.getAge();
		console.log(this.age);
	}
	@Input() child_id: number;
	private child: Child;
	private age: number;
	private medical_conditions: string[];
}
