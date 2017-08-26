import { Component, Input } from '@angular/core';

@Component({
	selector: 'children-tab',
	templateUrl: './children-tab.component.html',
	styleUrls: ['./children-tab.component.css']
})
export class ChildrenTab {
	@Input() child_id = 1;//: number;
}
