import { Component, OnInit } from '@angular/core';
import { ParamMap } from '@angular/router';
import { DatePipe } from '@angular/common';

import { Child } from '../child';
import { RestService } from '../rest.service';

@Component({
	selector: 'child-details',
	templateUrl: "./child-details.component.html",
	styleUrls: ["./child-details.component.css"]
})
export class ChildDetails implements OnInit {
	constructor(
		private restService: RestService,
		private datePipe: DatePipe
	) {}
	ngOnInit(): void {
		this.restService.getChild(1).then(child => this.child = child);
	}
	saveChild(): void {
		this.restService.updateChild(this.child);
	}
	deleteChild(): void {
		//this.restService.deleteChild(this.child.id); // Add warning
		console.log(this.child.birth_date);
	}

	setDoB(date): void {
		this.child.birth_date = this.datePipe.transform(date, 'yyyy-MM-dd');
	}
	private child: Child;
}
