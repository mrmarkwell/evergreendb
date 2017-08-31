import { Component, OnInit, OnChanges, EventEmitter, Output, Input } from '@angular/core';
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
export class ChildList implements OnInit, OnChanges {
    ngOnInit(): void {
    }
    ngOnChanges(): void {
        this.notifySelected.emit(null);
    }

    allChildren: Child[] = [
        { id: 1, name: "Bill" },
        { id: 2, name: "Bob" },
        { id: 3, name: "Lilly" },
        { id: 4, name: "Eden" },
        { id: 5, name: "Nora" },
    ]
    onSelect(child: Child): void {
        this.selectedChild = child
        this.notifySelected.emit(child);
    }

    onKey(event: any) {
        this.filteredChildren = this.allChildren.filter(Child => Child.name.toLowerCase().indexOf(event.target.value.toLowerCase()) !== -1)
    }

    filteredChildren: Child[] = this.allChildren;
    selectedChild: Child;
    @Output() notifySelected = new EventEmitter<Child>();
}
