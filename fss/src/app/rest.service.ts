import {Injectable} from '@angular/core';
import {Http, Headers} from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Child } from './child';

@Injectable()
export class RestService {
	constructor(private http: Http) {}

	getChildren(): Promise<Child[]> {
		let childrenUrl = this.evergreenUrl + '/entity/fss_child';
		console.log(childrenUrl);
		return this.http.get(childrenUrl)
			.toPromise().then(response => response.json() as Child[])
			.catch(this.handleError);
	}
	private handleError(error: any): Promise<any> {
		console.error('An error occurred', error);
		return Promise.reject(error.message || error);
	}

	private evergreenUrl = 'http://127.0.0.1:5000';
	private headers = new Headers({'Content-Type': 'application/json'});
}
