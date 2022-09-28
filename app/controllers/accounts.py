from pydantic import BaseModel

from fastapi import APIRouter


accounts_controller: APIRouter = APIRouter(prefix="/accounts")


class AccountData(BaseModel):
    id: int | None


@accounts_controller.get("/summary")
async def get_summary():
    # TODO: There should be summary for current period & all the time.
    #       It should include `Balance`, `Income` & `Outcome` only.

    pass

@accounts_controller.get("/last-7-days")
async def get_last_7_days_highlight():
    pass

@accounts_controller.get("/monthly-trend")
async def get_monthly_trend():
    pass

@accounts_controller.get("/balances")
async def get_balances():
    pass

@accounts_controller.get("/list")
async def get_accounts():
    pass

@accounts_controller.post("/create")
async def create_account(account_data: AccountData):
    pass

@accounts_controller.put("/update")
async def update_account(account_data: AccountData):
    pass

@accounts_controller.delete("/delete")
async def delete_account(id: int):
    pass
