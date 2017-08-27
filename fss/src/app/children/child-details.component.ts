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
		this.restService.getChild(1).then(child => {this.child = child; this.age = child.getAge()});
	}
	saveChild(): void {
		this.restService.updateChild(this.child);
	}
	deleteChild(): void {
		//this.restService.deleteChild(this.child.id); // Add warning
		console.log(this.child.birth_date);
	}

	setDoB(date): void {
		// Two problems. 1) date not displayed in right format causing date to be displayed wrong because of timezone
		//               2) Age doesn't seem to be right around birthday, might have to do more complicated method based on string
		console.log(date);
		this.child.birth_date = this.datePipe.transform(date, 'yyyy-MM-dd');
		console.log(this.child.birth_date);
		this.age = this.child.getAge();
		console.log(this.age);
	}
	private child: Child;
	private age: number;
}
