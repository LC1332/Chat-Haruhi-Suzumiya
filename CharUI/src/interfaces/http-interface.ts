import type { CodeEnum } from "../enums/http-enum";

// 统一的 HTTP 响应结构
export interface HTTPStruct<T> {
  code: CodeEnum;
  msg: string;
  result: T;
}
