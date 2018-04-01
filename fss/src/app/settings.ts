export class Settings {
    current_username: string;
    current_password: string;
    save_notify_interval: number;
    evergreen_url: string;

    public setDevMode(dev_mode: boolean) {
        if (dev_mode) {
            this.evergreen_url = "http://127.0.0.1:5000"
        } else {
            this.evergreen_url = "https://backend.matthewmarkwell.com"
            // this.evergreen_url = "http://ec2-54-193-44-138.us-west-1.compute.amazonaws.com";
        }
    }
}
