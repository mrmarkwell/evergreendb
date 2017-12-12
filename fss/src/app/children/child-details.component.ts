import { Component, OnInit, OnChanges, Input, Output, EventEmitter, ViewChild } from '@angular/core';
import { ParamMap } from '@angular/router';
import { DatePipe } from '@angular/common';
import { DomSanitizer } from '@angular/platform-browser';
import { MatIconRegistry } from '@angular/material';
import { FileUploader, FileItem, FileUploaderOptions, FileLikeObject } from 'ng2-file-upload';
import { MatSnackBar } from '@angular/material';


import { Child } from '../child';
import { RestService } from '../rest.service';

@Component({
    selector: 'child-details',
    templateUrl: "./child-details.component.html",
    styleUrls: ["./child-details.component.scss"]
})
export class ChildDetails implements OnInit, OnChanges {
    private age: string;
    private medical_conditions: string[];
    private child_status: string[];
    private child_photo_url: string;
    private on_changes_count = 0;
    private uploader: FileUploader;
    child: Child;

    @ViewChild('fileInput') fileInput: any;
    private allowed_mime_type = ['image/png', 'image/jpg', 'image/jpeg'];
    public hasBaseDropZoneOver: boolean = false;

    @Output() notifyDeleted = new EventEmitter<null>();
    constructor(
        iconRegistry: MatIconRegistry,
        sanitizer: DomSanitizer,
        private restService: RestService,
        private datePipe: DatePipe,
        public snackBar: MatSnackBar
    ) {
        iconRegistry.addSvgIcon(
            'trash_icon',
            sanitizer.bypassSecurityTrustResourceUrl('assets/trash_icon.svg'));
        iconRegistry.addSvgIcon(
            'save_icon',
            sanitizer.bypassSecurityTrustResourceUrl('assets/save_icon.svg'));
        iconRegistry.addSvgIcon(
            'star_icon',
            sanitizer.bypassSecurityTrustResourceUrl('assets/star_icon.svg'));
    }
    ngOnInit(): void {
        this.uploader = new FileUploader({
            url: this.restService.getPhotoUploadUrl(),
            itemAlias: 'photos',
            allowedMimeType: this.allowed_mime_type
        });
        this.uploader.onWhenAddingFileFailed = (file: FileLikeObject, filter: any, options: any) => {
            this.snackBar.open("Invalid File Type!", null, {
                duration: 2000
            })
        }
        this.uploader.onAfterAddingAll = (files: FileItem[]) => {
            files.forEach(fileItem => {
                fileItem.file.name = `child${this.child_id}.jpeg`;
            })
            this.uploader.uploadAll();
        }
        this.uploader.onCompleteItem = (file: FileItem, message: string, status: number) => {
            let snackbar_message: string;
            if (status != 201) {
                snackbar_message = "Error uploading file!";
            } else {
                snackbar_message = "Image uploaded!";
            }
            this.snackBar.open(snackbar_message, null, {
                duration: 2000,
            });
            this.fileInput.nativeElement.value = '';
            this.ngOnChanges();
        }
        this.restService.getEnum("fss_medical_condition").then(conditions => this.medical_conditions = conditions);
        this.restService.getEnum("fss_child_status").then(status => this.child_status = status);
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges());
        this.child_photo_url = this.restService.getChildPhotoUrl(this.child_id);
    }
    ngOnChanges(): void {
        this.restService.getChild(this.child_id).then(child => {
            if (child == undefined) return;
            this.child = child;
            this.age = this.getAgeStr()
            this.child.birth_date_object = this.restService.getDateFromString(this.child.birth_date)
        });
        this.child_photo_url = this.restService.getChildPhotoUrl(this.child_id) + "?" + this.on_changes_count++;
    }
    saveChild(): void {
        this.child.birth_date = this.restService.getStringFromDate(this.child.birth_date_object);
        this.restService.updateChild(this.child);
    }
    deleteChild(): void {
        if (confirm("Are you sure you want to delete this child and all associated data?")) {
            this.restService.deleteChild(this.child.id);
            this.child = null;
            this.notifyDeleted.emit();
        }
    }

    @Input() child_id: number;

    getAgeStr(): string {
        let age = this.child.getAge()
        return age === null? null: "Age: " + age
    }

    public picOverBase(e: any): void {
        this.hasBaseDropZoneOver = e;
    }

    public fileDropped(files: File[]): void {
        console.log("got a file");
        if (!files || files.length == 0) {
            console.log("No file in the file list!!");
        } else {
            console.log("Sending file to backend");
            console.log(files)
            this.uploader.uploadAll();
        }
    }

    // Dirty hack to style <input type=file> with angular meterial. Also can use label and style that, but that doesn't work well with angular meterial
    public openFileSelect(): void {
        document.getElementById("profile-pic-file-select").click();
    }
}
