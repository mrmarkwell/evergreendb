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
    }

    ngOnChanges(): void {
        this.getChildren()
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
    }

    constructor(private restService: RestService) {

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
    filterChildren(event: any = null) {
        if (event) {
            this.filteredChildren = this.allChildren.filter(Child => Child.child_pinyin_name.toLowerCase().indexOf(event.target.value.toLowerCase()) !== -1)
        } else {
            this.filteredChildren = this.allChildren;
        }
    }


}
