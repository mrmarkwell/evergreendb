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
		// Implement this function...
	}
	getChild(): void {
		this.restService.getChild(this.child_id).then(child => this.child = child);
	}
	getProjectedPathway(): void {
		this.restService.getProjectedPathway(this.child_id).then(pathway => this.dataSource.projectedPathway = pathway);
	}


}

export class PathwayDataSource extends DataSource<any> {

	projectedPathway: ProjectedPathway[];

	/** Connect function called by the table to retrieve one stream containing the data to render. */
	connect(): Observable<ProjectedPathway[]> {
		return Observable.of(this.projectedPathway);
	}

	disconnect() { }
}