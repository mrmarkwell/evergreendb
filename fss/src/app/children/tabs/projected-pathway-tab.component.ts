import { Component, OnChanges, OnInit, Input } from '@angular/core';
import { DataSource } from '@angular/cdk/collections';
import { Observable } from 'rxjs/Observable';
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


	@Input() child_id: number;

	constructor(
		private restService: RestService
	) { }
	ngOnInit(): void {
		this.getChild();
		this.getProjectedPathway();
		this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
	}

	ngOnChanges(): void {
		this.getChild();
		this.getProjectedPathway();
	}

	displayedColumns = ['stepNumber', 'shortDescription', 'details', 'completionDate'];
	dataSource = new PathwayDataSource();

	save(): void {
		for (let pathway of this.dataSource.projectedPathway) {
			// Update the pathway completion date with the object that is tied to the datepicker.
			pathway.pathway_completion_date = this.formatDate(pathway.pathway_completion_date_object);
			this.restService.updateProjectedPathway(pathway);
		}
	}

	formatDate(date: Date): string {
		let day = date.getDate();
		let month = date.getMonth() + 1;
		let year = date.getFullYear();
		let date_string = year + "-" + month + "-" + day;

		console.log("formatDate: Date string: ", date.toString());
		console.log("formatDate: Date Formatted string", date_string);
		return date_string;
	}

	getChild(): void {
		this.restService.getChild(this.child_id).then(child => this.child = child);
	}
	getProjectedPathway(): void {
		this.restService.getProjectedPathway(this.child_id).then(pathway => {
			this.dataSource.projectedPathway = pathway

			// Clear the pathway completion dates dictionary before recreating it.
			//this.dataSource.pathwayCompletionDates = {};
			for (let pathway of this.dataSource.projectedPathway) {
				let theDate = new Date(pathway.pathway_completion_date.replace(/-/g, '\/').replace(/T.+/, ''));
				console.log("Pathway Completion Date Object before assignment: ", pathway.pathway_completion_date_object);

				//this.dataSource.pathwayCompletionDates[pathway.id] = theDate;
				pathway.pathway_completion_date_object = theDate;
				console.log("Pathway Completion Date String: ", pathway.pathway_completion_date);
				console.log("Pathway Completion Date Object: ", theDate);
				console.log("Pathway Completion Date Object Local Time: ", theDate.toString());
			}
		});
	}


}

// Create a type for storing projectedPathway ID to Date object mappings.
export interface pathwayCompletionDate {
	[pathwayID: number]: Date;
}

export class PathwayDataSource extends DataSource<any> {

	projectedPathway: ProjectedPathway[];
	//pathwayCompletionDates: pathwayCompletionDate = {};

	/** Connect function called by the table to retrieve one stream containing the data to render. */
	connect(): Observable<ProjectedPathway[]> {
		return Observable.of(this.projectedPathway);
	}

	disconnect() { }
}