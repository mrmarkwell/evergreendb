import { Component, Input } from '@angular/core';

@Component({
	selector: 'child-tabs',
	templateUrl: './child-tabs.component.html'
})
export class ChildTabs {
	@Input() child_id: number;
}
