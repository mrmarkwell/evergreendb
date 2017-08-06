import { Component, OnInit } from '@angular/core';
import { ParamMap } from '@angular/router';

import { Child } from '../child';
import { RestService } from '../rest.service';

@Component({
	selector: 'child-details',
	templateUrl: "./child-details.component.html",
	styleUrls: ["./child-details.component.css"]
})
export class ChildDetails implements OnInit {
	constructor(
		private restService: RestService
	) {}
	ngOnInit(): void {
		this.restService.getChildren().then(children => this.children = children);
	}
	private children: Child[];
	private child: Child;
}
