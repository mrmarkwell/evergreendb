import { Component } from '@angular/core';
import { Child } from './child';

@Component({
	selector: 'child-list',
	template: `
		<h3>type in bar to search by name</h3>
		<input (keyup)="onKey($event)">
		<p>{{values}}</p>
	  <ul class="children">
	    <li *ngFor="let child of filteredChildren"
		    [class.selected]="child === selectedChild"
		    (click)="onSelect(child)">
		    <span class="id">{{child.id}}</span> {{child.name}}
		  </li>
	  </ul>				
	`,

	styles: [`
	   .selected {
      background-color: #CFD8DC !important;
      color: white;
    }
	`
	]
})
export class ChildList {

	allChildren: Child[] = [
		{ id: 1, name: "Bill" },
		{ id: 2, name: "Bob" },
		{ id: 3, name: "Lilly" },
		{ id: 4, name: "Eden" },
		{ id: 5, name: "Nora" },
	]

	filteredChildren: Child[] = this.allChildren;

	selectedChild: Child;

	onSelect(child: Child): void {
		this.selectedChild = child
	}

	onKey(event: any) {
		this.filteredChildren = this.allChildren.filter(Child => Child.name.toLowerCase().indexOf(event.target.value.toLowerCase()) !== -1)
	}
}
