import { Component, OnInit, OnChanges, Input, Output, EventEmitter } from '@angular/core';
import { ParamMap } from '@angular/router';
import { DatePipe } from '@angular/common';
import { DomSanitizer } from '@angular/platform-browser';
import { MdIconRegistry } from '@angular/material';
import { FileUploader } from 'ng2-file-upload';

import { Child } from '../child';
import { RestService } from '../rest.service';

const URL = 'https://127.0.0.1';

@Component({
    selector: 'child-details',
    templateUrl: "./child-details.component.html",
    styleUrls: ["./child-details.component.css"]
})
export class ChildDetails implements OnInit, OnChanges {
    @Output() notifyDeleted = new EventEmitter<null>();
    constructor(
        iconRegistry: MdIconRegistry,
        sanitizer: DomSanitizer,
        private restService: RestService,
        private datePipe: DatePipe
    ) {
        iconRegistry.addSvgIcon(
            'trash_icon',
            sanitizer.bypassSecurityTrustResourceUrl('assets/trash_icon.svg'));
        iconRegistry.addSvgIcon(
            'save_icon',
            sanitizer.bypassSecurityTrustResourceUrl('assets/save_icon.svg'));
    }
    ngOnInit(): void {
        this.restService.getEnum("fss_medical_condition").then(conditions => this.medical_conditions = conditions);
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
    }
    ngOnChanges(): void {
        this.restService.getChild(this.child_id).then(child => {
            if (child == undefined) return;
            this.child = child;
            this.age = child.getAge()
            this.child.birth_date_object = this.restService.getDateFromString(this.child.birth_date)
        });
    }
    saveChild(): void {
        this.child.birth_date = this.restService.getStringFromDate(this.child.birth_date_object);
        this.restService.updateChild(this.child);
    }
    deleteChild(): void {
        if (confirm("Are you sure you want to delete this child and all associated data?")) {
            //TODO: Delete associated family members, pathways, and interactions
            console.log("MYDEBUGMESSAGE");
            console.log(this.child);
            this.restService.deleteChild(this.child.id);
            this.child = null;
            this.notifyDeleted.emit();
        }
    }


	@Input() child_id: number;
	
	private child: Child;
	private age: number;
	private medical_conditions: string[];
	public uploader:FileUploader = new FileUploader( {url: URL} );
	public hasBaseDropZoneOver:boolean = false;
	public picOverBase(e:any):void {
		this.hasBaseDropZoneOver = e;
	}

	public fileDropped(files:File[]):void {
		console.log("got a file");
        if (files.length == 0) {
            console.log("No file in the file list!!");
        } else {
            console.log("Sending file to backend");
           // this.restService.uploadChildPhoto(files[0]);
        }
        console.log(files)
	}
}
