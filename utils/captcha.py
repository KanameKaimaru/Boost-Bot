import httpx
from config.config import load_config
from utils.logger import setup_logger

class CaptchaSolver:
    def __init__(self):
        self.config = load_config()
        self.logger = setup_logger()
        self.api_key = self.config["captcha_solver"].get("hcoptcha_api_key") or \
                      self.config["captcha_solver"].get("capsolver_api_key") or \
                      self.config["captcha_solver"].get("csolver_key") or \
                      self.config["captcha_solver"].get("dchcaptcha_api_key")
        self.service = self.config["captcha_solver"].get("use", "hcoptcha")
        self.max_retries = self.config["captcha_solver"].get("max_retries", 5)

    def solve_captcha(self):
        if not self.config["captcha_solver"]["solve_captcha"]:
            self.logger.warning("Captcha solving is disabled")
            return None
        
        for attempt in range(self.max_retries):
            try:
                if self.service == "hcoptcha":
                    return self.solve_hcaptcha()
                elif self.service == "capsolver":
                    return self.solve_capsolver()
                elif self.service == "csolver":
                    return self.solve_csolver()
                elif self.service == "dchcaptcha":
                    return self.solve_dchcaptcha()
            except Exception as e:
                self.logger.error(f"Captcha solving attempt {attempt + 1} failed: {e}")
                continue
        self.logger.error("Failed to solve captcha after max retries")
        return None

    def solve_hcaptcha(self):
        response = httpx.post(
            "https://api.hcaptcha.com/solve",
            json={
                "key": self.api_key,
                "sitekey": "4c672d35-0701-42b2-88c3-78380b0db560",  # Discord's hCaptcha sitekey
                "pageurl": "https://discord.com"
            }
        )
        if response.status_code == 200 and response.json().get("success"):
            return response.json().get("captcha_key")
        self.logger.error("hCaptcha solving failed")
        return None

    def solve_capsolver(self):
        response = httpx.post(
            "https://api.capsolver.com/createTask",
            json={
                "clientKey": self.api_key,
                "task": {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": "https://discord.com",
                    "websiteKey": "4c672d35-0701-42b2-88c3-78380b0db560"
                }
            }
        )
        if response.status_code == 200 and response.json().get("taskId"):
            task_id = response.json().get("taskId")
            for _ in range(10):
                result = httpx.post(
                    "https://api.capsolver.com/getTaskResult",
                    json={"clientKey": self.api_key, "taskId": task_id}
                ).json()
                if result.get("status") == "ready":
                    return result.get("solution", {}).get("gRecaptchaResponse")
                httpx.sleep(5)
        self.logger.error("Capsolver solving failed")
        return None

    def solve_csolver(self):
        response = httpx.post(
            "https://api.csolver.com/v1/captcha",
            json={
                "apiKey": self.api_key,
                "type": "hcaptcha",
                "siteKey": "4c672d35-0701-42b2-88c3-78380b0db560",
                "siteUrl": "https://discord.com"
            }
        )
        if response.status_code == 200 and response.json().get("captchaKey"):
            return response.json().get("captchaKey")
        self.logger.error("Csolver solving failed")
        return None

    def solve_dchcaptcha(self):
        response = httpx.post(
            "https://api.dchcaptcha.com/solve",
            json={
                "key": self.api_key,
                "sitekey": "4c672d35-0701-42b2-88c3-78380b0db560",
                "url": "https://discord.com"
            }
        )
        if response.status_code == 200 and response.json().get("solution"):
            return response.json().get("solution")
        self.logger.error("DCHcaptcha solving failed")
        return None