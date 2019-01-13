import { Component, OnInit, OnChanges, EventEmitter, Output, Input } from '@angular/core';
import { RestService } from '../rest.service';
import { Child } from '../child';
import { SearchCategory } from 'app/search-category';

@Component({
    selector: 'child-list',
    templateUrl: 'child-list.component.html',
    styleUrls: ['child-list.component.scss']
})

export class ChildList implements OnInit, OnChanges {
    allChildren: Child[];
    filteredChildren: Child[];
    selectedChild: Child;
    filterActive: Boolean = true;
    filterInSitu: Boolean = false;
    filterResolved: Boolean = false;
    filterCurrent: Boolean = false;
    filterUnknown: Boolean = false;
    searchText: string;
    currentSearchCategory: SearchCategory = new SearchCategory("child_pinyin_name", "Pinyin Name");
    searchCategories: SearchCategory[] = new Array<SearchCategory>(
        new SearchCategory("child_pinyin_name", "Pinyin Name"),
        new SearchCategory("child_chinese_name", "Chinese Name"),
        new SearchCategory("nickname", "Nickname"),
        new SearchCategory("diagnosis", "Diagnosis")

    );
    @Output() notifySelected = new EventEmitter<number>();

    ngOnInit(): void {
        this.getChildren();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
    }

    ngOnChanges(): void {
        this.getChildren();
    }

    constructor(private restService: RestService) { }

    createNewChild(): void {
        let new_child = new Child(null);
        new_child.child_pinyin_name = "New Child";
        this.restService.addChild(new_child).then(the_child => this.onSelect(the_child));
        this.filterUnknown = true;
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
        if (child.status === "Active") {
            statusClass = "active";
        } else if (child.status === "Current") {
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
            this._filterChildrenWithString(event.target.value);
        } else {
            this._filterChildrenWithString(this.searchText);
        }
    }

    private _filterChildrenWithString(searchstring: string) {
        this.filteredChildren = this.allChildren.filter(Child => {
            // Case for unknown child status
            if ((Child.status == null || Child.status == undefined || Child.status == "")) {
                if (!this.filterUnknown) {
                    // The child has no status, and the "unknown" toggle is off. Filter this child out.
                    return false;
                }
            } else if (!this.buildStatusFilterArray().includes(Child.status)) {
                return false;
            }
            // Return true if the search box is empty
            if (!searchstring) {
                return true;
            }
            // Diagnosis needs to filter on two different fields
            if (this.currentSearchCategory.viewValue == "Diagnosis") {
                let ret = false;
                if (this.childHasValue(Child, "primary_diagnosis")) {
                    ret = Child.primary_diagnosis.toLowerCase().indexOf(searchstring.toLowerCase()) !== -1;
                }
                if (this.childHasValue(Child, "secondary_diagnosis")) {
                    ret = ret || Child.secondary_diagnosis.toLowerCase().indexOf(searchstring.toLowerCase()) !== -1;
                }
                return ret;
            }
            if (this.childHasValue(Child, this.currentSearchCategory.value)) {
                console.log("Child has the right value");
                return Child[this.currentSearchCategory.value].toLowerCase().indexOf(searchstring.toLowerCase()) !== -1
            }
            return false;
        })

    }

    childHasValue(child: Child, value: string) {
        if (child[value] != null && child[value] != undefined && child[value] != "") {
            return true;
        }
        return false;
    }

    buildStatusFilterArray(): String[] {
        let statusFilterArray = new Array<String>();
        if (this.filterActive) statusFilterArray.push("Active");
        if (this.filterCurrent) statusFilterArray.push("Current");
        if (this.filterInSitu) statusFilterArray.push("In Situ");
        if (this.filterResolved) statusFilterArray.push("Resolved");
        return statusFilterArray;
    }

    downloadAll(): void {
        this.restService.getReport('family.csv')
    }
}
