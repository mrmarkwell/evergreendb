import { Component, Input } from '@angular/core';
import { Child } from '../child';

@Component({
    selector: 'children-page',
    templateUrl: './children-page.component.html',
    styleUrls: ['./children-page.component.scss']
})
export class ChildrenPage {
    onSelect(child_id: number): void {
        this.child_id = child_id;
    }
    childDeleted(): void {
        this.child_id = null;
    }
    @Input() child_id: number;
}
