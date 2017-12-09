import { Component, OnInit, OnChanges, EventEmitter, Output, Input } from '@angular/core';
import { RestService } from '../rest.service';
import { Child } from '../child';

@Component({
    selector: 'child-list',
    templateUrl: 'child-list.component.html',
    styleUrls: ['child-list.component.scss']
})

export class ChildList implements OnInit, OnChanges {
    allChildren: Child[];
    filteredChildren: Child[];
    selectedChild: Child;
    @Output() notifySelected = new EventEmitter<number>();

    ngOnInit(): void {
        this.getChildren();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
    }

    ngOnChanges(): void {
        this.getChildren();
        // let the_new_child = this.allChildren.find(child => child.id == this.selectedChild.id);
        // if (the_new_child === undefined) {
        //     this.selectedChild = null;
        // } else {
        //     this.onSelect(the_new_child);
        // }
    }

    constructor(private restService: RestService) { }

    createNewChild(): void {
        let new_child = new Child(null);
        new_child.child_pinyin_name = "New Child";
        this.restService.addChild(new_child).then(the_child => this.onSelect(the_child));
    }

    isSelected(child): boolean {
        // Object equality doesn't work in js/ts. It just checks if instances are the same not contents are equal
        return this.selectedChild && child.id === this.selectedChild.id;
    }

    onSelect(child: Child): void {
        this.selectedChild = child;
        this.notifySelected.emit(child.id);
    }

    getChildren(): void {
        this.restService.getChildren().then(children => {
            this.allChildren = children;
            this.filterChildren();
            return this.allChildren;
        });
    }

    getChildStatusClass(child: Child): string {
        let statusClass = "";
        if(child.status === "Active") {
            statusClass = "active";
        } else if(child.status === "Current") {
            statusClass = "current";
        } else if (child.status === "In Situ") {
            statusClass = "in_situ"
        } else if (child.status === "Resolved") {
            statusClass = "resolved"
        } else {
            statusClass = "unknown"
        }
        return "status " + statusClass
    }

    filterChildren(event: any = null) {
        if (event) {
            this.filteredChildren = this.allChildren.filter(Child => Child.child_pinyin_name.toLowerCase().indexOf(event.target.value.toLowerCase()) !== -1)
        } else {
            this.filteredChildren = this.allChildren;
        }
    }


}
