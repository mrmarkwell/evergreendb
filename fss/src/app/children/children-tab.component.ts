import { Component, Input } from '@angular/core';
import { Child } from './child';

@Component({
	selector: 'children-tab',
	templateUrl: './children-tab.component.html',
	styleUrls: ['./children-tab.component.css']
})
export class ChildrenTab {
	onSelect(child: Child): void {
		this.child_id = child.id;
	  	}
	@Input() child_id = 1;//: number;
}
