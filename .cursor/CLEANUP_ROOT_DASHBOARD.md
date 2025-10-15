# 🧹 Cleanup: Редирект корневой страницы + Свернутый sidebar

## Проблема

У проекта было **две версии Dashboard**:
1. **`/`** (app/page.tsx) - использовала mock данные `getMockStats()`
2. **`/dashboard`** (app/dashboard/page.tsx) - использовала реальный API ✅

Это создавало путаницу и требовало поддержки двух версий.

## Решение

### 1. Редирект с `/` на `/dashboard`

**Файл:** `dashboard/app/page.tsx`

**Было:** ~110 строк кода с mock данными и отдельным UI

**Стало:** 5 строк с редиректом
```typescript
import { redirect } from "next/navigation"

export default function Home() {
  redirect("/dashboard")
}
```

**Результат:**
- ✅ Пользователи всегда попадают на актуальный dashboard с API
- ✅ HTTP 307 Temporary Redirect с `/` на `/dashboard`
- ✅ Убрана поддержка устаревшей версии с mock данными
- ✅ Единая точка входа в приложение

### 2. Sidebar по умолчанию свернут

**Файл:** `dashboard/app/dashboard/page.tsx`

**Добавлено:** `defaultOpen={false}` в `SidebarProvider`

```typescript
<SidebarProvider
  defaultOpen={false}  // <- новая строка
  style={{
    "--sidebar-width": "calc(var(--spacing) * 72)",
    "--header-height": "calc(var(--spacing) * 12)",
  } as React.CSSProperties}
>
```

**Результат:**
- ✅ При первой загрузке sidebar свернут
- ✅ Больше места для контента (карточки и график)
- ✅ Пользователь может развернуть sidebar кнопкой Toggle

## Преимущества

### Редирект:
1. **Единая версия** - все используют dashboard с реальным API
2. **Проще поддержка** - нет двух версий UI
3. **Меньше кода** - удалено ~105 строк устаревшего кода
4. **Нет путаницы** - одна точка входа

### Свернутый sidebar:
1. **Больше места** - на малых экранах важно пространство
2. **Фокус на данных** - метрики и график занимают больше места
3. **Лучший UX** - пользователь может развернуть по необходимости

## Удаленные зависимости из старой страницы

Теперь можно удалить неиспользуемые компоненты (если они не используются где-то еще):
- `components/overview-cards.tsx`
- `components/message-chart.tsx`
- `lib/mock-data.ts`

**Примечание:** Не удаляем автоматически, нужно проверить использование.

## Проверка

### Редирект:
```bash
curl -I http://localhost:3000/
# Должен вернуть: HTTP/1.1 307 Temporary Redirect
# Location: /dashboard
```

### Sidebar:
1. Открыть http://localhost:3000 (должен редиректнуть на /dashboard)
2. ✅ Sidebar должен быть свернут при первой загрузке
3. ✅ Кнопка Toggle (слева вверху) разворачивает sidebar
4. ✅ Состояние сохраняется в localStorage

## TypeScript проверка

```bash
cd dashboard && pnpm type-check
```

✅ Результат: 0 ошибок

## Дата изменения

2025-10-15

