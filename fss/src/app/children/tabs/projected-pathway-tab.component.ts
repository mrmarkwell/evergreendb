import { Component, OnChanges, OnInit, Input } from '@angular/core';
import { DataSource } from '@angular/cdk/collections';
import { Observable } from 'rxjs/Observable';
import { DomSanitizer } from '@angular/platform-browser';
import { MdIconRegistry } from '@angular/material';
import 'rxjs/add/observable/of';

import { Child } from '../../child';
import { ProjectedPathway } from '../../projected-pathway';
import { RestService } from '../../rest.service';

@Component({
	selector: 'projected-pathway-tab',
	templateUrl: './projected-pathway-tab.component.html'
})


export class ProjectedPathwayTabComponent implements OnInit, OnChanges {
	private child: Child;
	projectedPathways: ProjectedPathway[];

	@Input() child_id: number;

	constructor(
		iconRegistry: MdIconRegistry,
		sanitizer: DomSanitizer,
		private restService: RestService) {
		iconRegistry.addSvgIcon(
			'trash_icon',
			sanitizer.bypassSecurityTrustResourceUrl('assets/trash_icon.svg'));
	}

	ngOnInit(): void {
		this.getChild();
		this.getProjectedPathways();
		this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
	}

	ngOnChanges(): void {
		this.getChild();
		this.getProjectedPathways();
	}

	save(): void {
		for (let pathway of this.projectedPathways) {
			// Update the pathway completion date with the object that is tied to the datepicker.
			pathway.pathway_completion_date = this.restService.getStringFromDate(pathway.pathway_completion_date_object);	
			this.restService.updateProjectedPathway(pathway);
		}
	}

	delete(pathway_id: number): void {
		this.restService.deleteProjectedPathway(pathway_id);
	}

	addNewStep(): void {
		let next_step = 1;
		let latest_pathway = this.projectedPathways.slice(-1)[0];
		if (latest_pathway) {
			next_step = latest_pathway.pathway_step_number + 1;
		}
		let new_pathway = new ProjectedPathway();
		new_pathway.pathway_step_number = next_step;
		new_pathway.child_id = this.child_id;
		this.restService.addProjectedPathway(new_pathway);

	}



	getChild(): void {
		this.restService.getChild(this.child_id).then(child => this.child = child);
	}
	getProjectedPathways(): void {
		this.restService.getProjectedPathway(this.child_id).then(pathways => {
			// Sort them by step number
			pathways.sort(
				function (a, b) {
					return (a.pathway_step_number > b.pathway_step_number) ? 1
						: ((a.pathway_step_number < b.pathway_step_number) ? -1
							: 0);
				}
			);
			this.projectedPathways = pathways;
			let step_number = 1;
			for (let pathway of this.projectedPathways) {
				// Reset the pathway numbers to increment starting at 1.
				// This ensures that the steps are numbered appropriately even if steps are deleted. 
				pathway.pathway_step_number = step_number++;

				// Make a Date object for the pathway_completion_date. Datepicker wants to be tied to a date object.
				if (pathway.pathway_completion_date) {
					let theDate = this.restService.getDateFromString(pathway.pathway_completion_date);

					pathway.pathway_completion_date_object = theDate;
				}
				else {
					pathway.pathway_completion_date_object = null;
				}
			}
			for (let p of this.projectedPathways) {
				console.log(p)
			}
		});
	}


}
