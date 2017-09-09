import { Component, Input } from '@angular/core';
import { Child } from '../child';

@Component({
	selector: 'children-tab',
	templateUrl: './children-tab.component.html',
	styleUrls: ['./children-tab.component.css']
})
export class ChildrenTab {
	onSelect(child_id: number): void {
		this.child_id = child_id;
	  	}
	@Input() child_id: number;
}
